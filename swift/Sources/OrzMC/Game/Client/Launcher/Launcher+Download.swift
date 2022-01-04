//
//  File.swift
//  
//
//  Created by joker on 2022/1/3.
//

import Mojang
import JokerKits
import Foundation
import ConsoleKit

extension Launcher {
    
    /// 下载游戏客户端jar文件
    func downloadClient() async throws {
        guard let startInfo = self.startInfo, let client = try await startInfo.version.gameInfo?.downloads.client
        else {
            return
        }
        try await self.download(
            client.url,
            progressHint: "下载客户端文件: \(client.url.lastPathComponent)",
            targetDir: GameDir.clientVersionDir(version: startInfo.version.id),
            hash: client.sha1)
    }
    
    /// 下载游戏客户端资源文件
    func downloadAssets() async throws {
        guard let startInfo = self.startInfo, let objects = try await startInfo.version.gameInfo?.assetIndex.assetInfo?.objects
        else {
            return
        }
        
        var count = 0
        let total = objects.count
        
        for filename in objects.keys {
            count += 1
            guard let info = objects[filename]
            else {
                continue
            }
            let assetObjURL = Mojang.assetObjURL(info.path())
            try await self.download(
                assetObjURL,
                progressHint: "下载资源文件(\(count)/\(total))：\(filename)",
                targetDir: GameDir.assetsObj(version: startInfo.version.id, path: info.path()),
                hash: info.hash
            )
        }
    }
    
    /// 下载游戏客户端jar库文件
    func downloadLibraries() async throws {
        guard let startInfo = self.startInfo, let libraries = try await startInfo.version.gameInfo?.libraries
        else{
            return
        }
        
        var count = 0
        let total = libraries.count
        
        for lib in libraries {
            count += 1
            
            // 获取需要下载的库
            var artifact = lib.downloads.artifact
            var targetDir = GameDir.libraryObj(version: startInfo.version.id, path: artifact.path)
            var libName = lib.name
            
            let currentOSName = Platform.current().platformName()
            if let natives = lib.natives, let nativeClassifier = natives[currentOSName], let nativeArtifact = lib.downloads.classifiers?[nativeClassifier] {
                artifact = nativeArtifact
                targetDir = GameDir.clientVersionNativeDir(version: startInfo.version.id, path: nativeClassifier)
                libName = [lib.name, nativeClassifier].joined(separator: ":")
            }
            
            // 判断当前平台是否需要下载
            var allowDownload = true
            if let rules = lib.rules {
                var allowOSSet = Set<String>()
                rules.forEach { rule in
                    if rule.action == "allow" {
                        if let osname = rule.os?.name {
                            allowOSSet.insert(osname)
                        }
                        else {
                            allowOSSet.insert(currentOSName)
                        }
                    }
                    else if rule.action == "disallow", let osName = rule.os?.name {
                        allowOSSet.remove(osName)
                    }
                }
                allowDownload = allowOSSet.contains(currentOSName)
            }
            
            if lib.rules == nil, let natives = lib.natives, !natives.keys.contains(currentOSName) {
                allowDownload = false
            }
            
            guard allowDownload
            else {
                let info = "下载库文件(\(count)/\(total))：\(lib.name)".consoleText() + " [Not Need]".consoleText(.info)
                console.output(info)
                continue
            }
            
            try await self.download(
                artifact.url,
                progressHint: "下载库文件(\(count)/\(total))：\(libName)",
                targetDir: targetDir,
                hash: artifact.sha1
            )
        }
    }
}

extension Platform {
    func platformName() -> String {
        switch self {
        case .linux:
            return "linux"
        case .windows:
            return "windows"
        case .macosx:
            return "osx"
        default:
            return "unsupported"
        }
    }
}

extension Launcher {
    
    /// 下载文件
    /// - Parameters:
    ///   - url: 文件URL
    ///   - progressHint: 下载进度提示文字
    ///   - targetDir: 下载后放入的目录
    private func download(_ url: URL, progressHint: String?, targetDir: GameDir, hash: String) async throws {
        return try await withCheckedThrowingContinuation { continuation in
            var progressBar: ActivityIndicator<ProgressBar>? = nil
            let showProgress = progressHint != nil
            if showProgress {
                progressBar = console.progressBar(title: progressHint!)
            }
            
            let toFilePath = targetDir.filePath(url.lastPathComponent)
            
            // 已经下载过的，且校验完整的文件，不重复下载
            do {
                if FileManager.default.fileExists(atPath: toFilePath) {
                    let sha1 = try URL(fileURLWithPath: toFilePath).fileSHA1Value
                    if sha1 == hash {
                        progressBar?.start()
                        progressBar?.succeed()
                        continuation.resume()
                        return
                    }
                }
            } catch let error {
                self.console.output(error.localizedDescription.consoleText(.error), newLine: true)
                continuation.resume(throwing: error)
            }
            
            progressBar?.start()
            Downloader().download(url) { [progressBar] progress, filePath in
                
                progressBar?.activity.currentProgress = progress
                
                if let fileURL = filePath {
                    progressBar?.succeed()
                    
                    do {
                        // Check SHA1 Value
                        let sha1 = try fileURL.fileSHA1Value
                        guard sha1 == hash
                        else {
                            throw URLError(.badServerResponse)
                        }
                        
                        // 移动文件
                        let fromFilePath = fileURL.path
                        try FileManager.moveFile(fromFilePath: fromFilePath, toFilePath: toFilePath, overwrite: true)
                        continuation.resume()
                    } catch let error {
                        self.console.output(error.localizedDescription.consoleText(.error), newLine: true)
                        continuation.resume(throwing: error)
                    }
                }
            }
        }
    }
}
