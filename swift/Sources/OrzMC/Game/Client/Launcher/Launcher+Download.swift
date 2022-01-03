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
        guard let startInfo = self.startInfo, let clientURL = try await startInfo.version.gameInfo?.downloads.client.url
        else {
            return
        }
        try await self.download(clientURL, progressHint: "下载客户端文件: \(clientURL.lastPathComponent)", targetDir: startInfo.gameDir)
    }
    
    /// 下载游戏客户端资源文件
    func downloadAssets() async throws {
        guard let startInfo = self.startInfo, let objects = try await startInfo.version.gameInfo?.assetIndex.assetInfo?.objects
        else {
            return
        }
        
        var count = 0;
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
                targetDir: GameDir.assetsObj(version: startInfo.version.id, path: info.path())
            )
        }
    }
    
    
    /// 下载游戏客户端jar库文件
    func downloadLibraries() async throws {
        
    }
}

extension Launcher {
    
    /// 下载文件
    /// - Parameters:
    ///   - url: 文件URL
    ///   - progressHint: 下载进度提示文字
    ///   - targetDir: 下载后放入的目录
    private func download(_ url: URL, progressHint: String?, targetDir: GameDir) async throws {
        
        let showProgress = progressHint != nil
        
        return try await withCheckedThrowingContinuation { continuation in
            
            var progressBar: ActivityIndicator<ProgressBar>? = nil
            if showProgress {
                progressBar = console.progressBar(title: progressHint!)
                progressBar?.start()
            }
            
            Downloader().download(url) { [progressBar] progress, filePath in
                
                if showProgress {
                    progressBar?.activity.currentProgress = progress
                }
                
                if let fromFilePath = filePath?.path {
                    progressBar?.succeed()
                    do {
                        let toFilePath = targetDir.filePath(url.lastPathComponent)
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
