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
        
        guard let startInfo = self.startInfo, let gameInfo = try await startInfo.version.gameInfo
        else {
            return
        }
        
        let jarExt = "jar"
        let cpSep = Platform.current() == .windows ? ";" : ":"
    
        let classPath = Array([
            GameDir.libraries(version: startInfo.version.id).dirPath,
            GameDir.clientVersionDir(version: startInfo.version.id).dirPath
        ].compactMap { FileManager.allFiles(in: $0, ext: jarExt) }.joined())
        
        let envs = [
            "natives_directory": "\(GameDir.clientVersionNativeDir(version: startInfo.version.id).dirPath)",
            "launcher_name": "OrzMC",
            "launcher_version": "\(startInfo.version.id)",
            "auth_player_name": "\(startInfo.username)",
            "version_name": "\(startInfo.version.id)",
            "game_directory": "\(GameDir.clientDir(version: startInfo.version.id).dirPath)",
            "assets_root": "\(GameDir.assets(version: startInfo.version.id).dirPath)",
            "assets_index_name": "\(try await startInfo.version.gameInfo?.assetIndex.id ?? "")",
            "auth_uuid": "\(UUID.init())",
            "auth_access_token": "\(UUID.init())",
//            "clientid": "\(startInfo.version.id)",
//            "auth_xuid": "\(startInfo.username)",
            "user_type": "mojang",
            "version_type": "\(startInfo.version.type)",
            "classpath": "\(classPath.joined(separator: cpSep))" ,
        ]
        
        let javaArgsArray = [
            "-Xms512M",
            "-Xmx2G",
            "-Djava.net.preferIPv4Stack=true",
            "-XstartOnFirstThread",
        ]
        
        // 处理jvm相关参数
        let jvmArgsArray = gameInfo.arguments.jvm.compactMap { (arg) -> String? in
            switch arg {
            case .object(_):
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
        Array([javaArgsArray, jvmArgsArray, [gameInfo.mainClass], gameArgsArray].joined()).forEach { arg in
            
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
        
        let javaPath = Shell.run(
            path: "/usr/bin/env",
            args: ["which", "java"]).trimmingCharacters(in: .whitespacesAndNewlines)
        
        print(Shell.run(path: javaPath, args: args))
    }
}
