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
    
    /// 下载启动器启动需要的文件
    public func download() async throws {
        try await downloadClient()
        try await downloadAssets()
        try await downloadLibraries()
    }
    
    /// 下载游戏客户端jar文件
    private func downloadClient() async throws {
        guard let startInfo = self.startInfo, let client = try await startInfo.version.gameInfo?.downloads.client
        else {
            return
        }
        
        // 下载版本信息JSON文件
        if let url = startInfo.version.url, let data = try await url.getData {
            let filePath = GameDir.clientVersionDir(version: startInfo.version.id).filePath(url.lastPathComponent)
            let fileURL = URL(fileURLWithPath: filePath)
            try data.write(to: fileURL)
        }
        
        // 下载版本Jar文件
        let filename = [startInfo.version.id, client.url.pathExtension].joined(separator: ".")
        try await self.download(
            client.url,
            progressHint: "下载客户端文件: \(filename)",
            targetDir: GameDir.clientVersionDir(version: startInfo.version.id),
            hash: client.sha1,
            filename: filename
        )
    }
    
    /// 下载游戏客户端资源文件
    private func downloadAssets() async throws {
        guard let startInfo = self.startInfo, let assetIndex = try await startInfo.version.gameInfo?.assetIndex, let objects = try await assetIndex.assetInfo?.objects
        else {
            return
        }
        
        // 下载资源索引文件json
        let indexFileName = assetIndex.url.lastPathComponent
        try await self.download(
            assetIndex.url,
            progressHint: "下载资源索引文件: \(indexFileName)",
            targetDir: .assetsIdx(version: startInfo.version.id),
            hash: assetIndex.sha1,
            filename: indexFileName
        )
        
        // 下载资源对象文件
        var count = 0
        let total = objects.count
        
        for filename in objects.keys {
            count += 1
            guard let info = objects[filename]
            else {
                continue
            }
            let assetObjURL = Mojang.assetObjURL(info.filePath())
            try await self.download(
                assetObjURL,
                progressHint: "下载资源文件(\(count)/\(total))：\(filename)",
                targetDir: GameDir.assetsObj(version: startInfo.version.id, path: info.dirPath()),
                hash: info.hash
            )
        }
    }
    
    /// 下载游戏客户端jar库文件
    private func downloadLibraries() async throws {
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
            let dirPath = NSString(string: artifact.path).deletingLastPathComponent
            var targetDir = GameDir.libraryObj(version: startInfo.version.id, path: dirPath)
            var libName = lib.name
            
            let currentOSName = Platform.current().platformName()
            if let natives = lib.natives, let nativeClassifier = natives[currentOSName], let nativeArtifact = lib.downloads.classifiers?[nativeClassifier] {
                artifact = nativeArtifact
                targetDir = GameDir.clientVersionNativeDir(version: startInfo.version.id)
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
