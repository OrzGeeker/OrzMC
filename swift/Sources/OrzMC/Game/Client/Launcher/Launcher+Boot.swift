//
//  File.swift
//  
//
//  Created by joker on 2022/1/5.
//

import Foundation
import JokerKits

extension Launcher {
    
    /// 启动客户端
    func launch() async throws {
        
        guard let gameInfo = try await self.clientInfo.version.gameInfo
        else {
            return
        }
        
        let jarExt = "jar"
        let cpSep = Platform.os() == .windows ? ";" : ":"
        
        let classPath = Array([
            GameDir.libraries(version: clientInfo.version.id).dirPath,
            GameDir.clientVersion(version: clientInfo.version.id).dirPath
        ].compactMap { FileManager.allFiles(in: $0, ext: jarExt) }.joined())
        
        
        let gameDir = GameDir.client(version: clientInfo.version.id).dirPath
        let envs = [
            "natives_directory": GameDir.clientVersionNative(version: clientInfo.version.id).dirPath,
            "launcher_name": "OrzMC",
            "launcher_version": clientInfo.version.id,
            "auth_player_name": clientInfo.username,
            "version_name": clientInfo.version.id,
            "game_directory": gameDir,
            "assets_root": GameDir.assets(version: clientInfo.version.id).dirPath,
            "assets_index_name": try await clientInfo.version.gameInfo?.assetIndex.id ?? "",
            "auth_uuid": UUID().uuidString,
            "auth_access_token": clientInfo.accessToken ?? UUID().uuidString,
            "clientid": clientInfo.version.id,
            "auth_xuid": clientInfo.username,
            "user_type": "mojang",
            "version_type": clientInfo.version.type,
            "classpath": classPath.joined(separator: cpSep),
            "path": GameDir.clientLogConfig(version: clientInfo.version.id).filePath(gameInfo.logging.client.file.id)
        ]
        
        var javaArgsArray = [
            "-Xms" + clientInfo.minMem,
            "-Xmx" + clientInfo.maxMem,
            "-Djava.net.preferIPv4Stack=true"
        ]
        
        if clientInfo.debug {
            javaArgsArray.append(gameInfo.logging.client.argument)
        }
        
        // 处理jvm相关参数
        let jvmArgsArray = gameInfo.arguments.jvm.compactMap { (arg) -> String? in
            switch arg {
            case .object(let obj):
                for rule in obj.rules {
                    if rule.os.name == Platform.os().platformName(), rule.action == "allow" {
                        switch obj.value {
                        case .array(let values):
                            return values.joined(separator: " ")
                        case .string(let value):
                            return value
                        }
                    }
                }
                return nil
            case .string(let value):
                return value
            }
        }
        
        // 处理游戏启动器参数
        let gameArgsArray = gameInfo.arguments.game.compactMap { (arg) -> String? in
            switch arg {
            case .object(_):
                return nil
            case .string(let value):
                return value
            }
        }
        
        //构造参数数组
        var args = [String]()
        
        let regex = try NSRegularExpression(pattern: "\\$\\{(\\w+)\\}", options: .caseInsensitive)
        Array([
            javaArgsArray,
            jvmArgsArray,
            [gameInfo.mainClass],
            gameArgsArray
        ].joined()).forEach { arg in
            
            let matches = regex.matches(in: arg, range: NSRange(location: 0, length: arg.count))
            var argValue = arg
            for m in matches {
                if let placeholderRange = Range(m.range(at: 0), in: arg), let envKeyRange = Range(m.range(at: 1),in: arg) {
                    let envPlaceholder = String(arg[placeholderRange])
                    let envKey = String(arg[envKeyRange])
                    if let envValue = envs[envKey] {
                        argValue = argValue.replacingOccurrences(of: envPlaceholder, with: envValue)
                    }
                    else {
                        argValue = argValue.replacingOccurrences(of: envPlaceholder, with: "")
                    }
                }
            }
            if argValue.count > 0 {
                args.append(argValue)
            }
        }
        
        if clientInfo.debug {
            for arg in args {
                print(arg)
            }
        }
        
        let javaPath = try Shell.run(
            path: "/usr/bin/env",
            args: ["which", "java"]).trimmingCharacters(in: .whitespacesAndNewlines)
        
        try Shell.run(path: javaPath, args: args, workDirectory: gameDir) { process in
            guard process.terminationStatus == 0
            else {
                print(process.terminationReason)
                return
            }
        }
        Platform.console.output("客户端正在启动请稍等...", style: .success)
    }
}
