//
//  File.swift
//  
//
//  Created by wangzhizhou on 2022/1/12.
//

import Mojang
import JokerKits

enum VanillaServerError: Error {
    case getServerInfoFailed
    case launchFailed
}

/// Vanilla 服务器
///
/// 启动命令示例:
/// ```bash
/// java -Xmx1024M -Xms1024M -jar minecraft_server.1.18.1.jar nogui
/// ```
///
/// 1. [官方部署服务器文档](https://www.minecraft.net/en-us/download/server)
/// 2. [部署服务器百科文档](https://minecraft.fandom.com/wiki/Tutorials/Setting_up_a_server)
///
/// 官方服务端文件下载速度太慢, 容易超时
struct VanillaServer: Server {
    
    let deployInfo: DeployInfo
    
    func start() async throws {
        
        guard let serverInfo = try await Mojang.manifest?.versions.filter({ $0.id == deployInfo.version }).first?.gameInfo?.downloads.server
        else {
            throw VanillaServerError.getServerInfoFailed
        }
        
        let fileName = serverInfo.url.lastPathComponent
        let targetDir = GameDir.server(version: deployInfo.version, type: GameType.vanilla.rawValue)
        let filePath = targetDir.filePath(fileName)
        let progressHint = "下载服务端文件：\(fileName)"
        try await GameUtils.download(
            serverInfo.url,
            progressHint: progressHint,
            targetDir: targetDir,
            hash: serverInfo.sha1)
        
        let javaPath = try Shell.run(
            path: "/usr/bin/env",
            args: ["which", "java"]).trimmingCharacters(in: .whitespacesAndNewlines)
        
         var args = [
            "-Xms512M",
            "-Xmx2G",
            "-jar",
            filePath
        ]
        
        if !deployInfo.gui {
            args.append("--nogui")
        }
        
        if deployInfo.debug {
            for arg in args {
                print(arg)
            }
        }

        try Shell.run(path: javaPath, args: args) { process in
            guard process.terminationStatus == 0
            else {
                print(process.terminationReason)
                return
            }
        }
        Platform.console.output("服务端正在启动请稍等...", style: .success)
    }
}
