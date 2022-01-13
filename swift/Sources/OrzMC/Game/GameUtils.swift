//
//  File.swift
//  
//
//  Created by wangzhizhou on 2022/1/13.
//

import Foundation
import ConsoleKit
import JokerKits

struct GameUtils {
    /// 下载文件
    /// - Parameters:
    ///   - url: 文件URL
    ///   - progressHint: 下载进度提示文字
    ///   - targetDir: 下载后放入的目录
    ///   - hash: 文件的SHA1哈希值
    ///   - filename: 下载后的转存文件名
    ///   - console: 控制台实例
    static func download(
        _ url: URL,
        progressHint: String?,
        targetDir: GameDir,
        hash: String,
        filename: String? = nil,
        console: Console = Platform.console
    ) async throws {
        return try await withCheckedThrowingContinuation { continuation in
            var progressBar: ActivityIndicator<ProgressBar>? = nil
            let showProgress = progressHint != nil
            if showProgress {
                progressBar = console.progressBar(title: progressHint!)
            }
            
            let toFilePath = targetDir.filePath(filename ?? url.lastPathComponent)
            
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
                console.output(error.localizedDescription.consoleText(.error), newLine: true)
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
                        console.output(error.localizedDescription.consoleText(.error), newLine: true)
                        continuation.resume(throwing: error)
                    }
                }
            }
        }
    }
}
