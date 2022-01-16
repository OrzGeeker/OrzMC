//
//  File.swift
//  
//
//  Created by wangzhizhou on 2022/1/16.
//

import Foundation
import JokerKits

extension Server {
    
    func launchServer(_ filePath: String, workDirectory: GameDir) async throws {
        let javaPath = try Shell.run(
            path: "/usr/bin/env",
            args: ["which", "java"]).trimmingCharacters(in: .whitespacesAndNewlines)
        
        var args = [
            "-Xms" + serverInfo.minMem,
            "-Xmx" + serverInfo.maxMem,
            "-jar",
            filePath
        ]
        
        if !serverInfo.gui {
            args.append("--nogui")
        }
        
        if serverInfo.forceUpgrade {
            args.append("--forceUpgrade")
        }
        
        if serverInfo.debug {
            for arg in args {
                print(arg)
            }
        }
        
        let eulaFilePath = workDirectory.filePath("eula.txt")
        if let eulaFileContent = try? String(contentsOfFile: eulaFilePath) {
            
            // 修改ELUA协议
            Platform.console.pushEphemeral()
            Platform.console.warning("首次启动，未同意EULA协议")
            try eulaFileContent.replacingOccurrences(of: "eula=false", with: "eula=true")
                .write(toFile: eulaFilePath, atomically: false, encoding: .utf8)
            Platform.console.popEphemeral()
            Platform.console.success("已同意EULA协议")
            
            // 修改服务器属性
            let propertiesFilePath = workDirectory.filePath("server.properties")
            if let propertiesFileConent = try? String(contentsOfFile: propertiesFilePath) {
                Platform.console.pushEphemeral()
                try propertiesFileConent.replacingOccurrences(of: "online-mode=true", with: "online-mode=false")
                    .write(toFile: propertiesFilePath, atomically: false, encoding: .utf8)
                Platform.console.popEphemeral()
                Platform.console.success("服务器运行为离线模式")
            }
            
            Platform.console.info("服务端正在运行中...")
            try Shell.run(path: javaPath, args: args, workDirectory: workDirectory.dirPath) { process in
                guard process.terminationStatus == 0
                else {
                    print(process.terminationReason)
                    return
                }
                Platform.console.info("服务端已停止")
            }
        }
        else {
            try await Shell.run(path: javaPath, args: args, workDirectory: workDirectory.dirPath)
            try await launchServer(filePath, workDirectory: workDirectory)
        }
    }
}
