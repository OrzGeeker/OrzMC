//
//  File.swift
//  
//
//  Created by joker on 2022/1/3.
//

import PaperMC
import JokerKits
import Foundation
import ConsoleKit

enum PaperServerError: Error {
    case versionRespFailed
    case convertBuildStringFailed
    case buildRespFailed
    case applicationFailed
    case downloadURLFailed
}

struct PaperServer: Server {
    
    let serverInfo: ServerInfo
        
    func start() async throws {
        
        let versionAPI = PaperMC.api.projects("paper").versions(serverInfo.version)
        guard let versionData = try await versionAPI.getData
        else {
            throw PaperServerError.versionRespFailed
        }
        
        let decoder = PaperMC.api.jsonDecoder
        let version = try decoder.decode(Version.self, from: versionData)
        
        guard let latestBuild = (version.builds.last as NSNumber?)?.stringValue
        else {
            throw PaperServerError.convertBuildStringFailed
        }
        let buildAPI = versionAPI.builds(latestBuild)
        guard let buildData = try await buildAPI.getData
        else {
            throw PaperServerError.buildRespFailed
        }
        
        let build = try decoder.decode(Build.self, from: buildData)
        
        
        guard let application = build.downloads["application"]
        else {
            throw PaperServerError.applicationFailed
        }
        
        guard let downloadURL = buildAPI.downloads(application.name).url
        else {
            throw PaperServerError.downloadURLFailed
        }
        
        let filename = downloadURL.lastPathComponent
        let targetDir = GameDir.server(version: serverInfo.version, type: GameType.paper.rawValue)
        let filePath = targetDir.filePath(filename)
        let progressHint = "下载服务端文件：\(filename)"
        
        try await GameUtils.download(
            downloadURL,
            progressHint: progressHint,
            targetDir: targetDir,
            hash: application.sha256,
            hashType: .sha256)
                
        try await launchServer(filePath, workDirectory: targetDir)
    }
    
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
            Platform.console.pushEphemeral()
            Platform.console.warning("首次启动，未同意EULA协议")
            try eulaFileContent.replacingOccurrences(of: "eula=false", with: "eula=true")
                .write(toFile: eulaFilePath, atomically: false, encoding: .utf8)
            Platform.console.popEphemeral()
            Platform.console.success("已同意EULA协议")
            
            Platform.console.info("服务端正在运行中...")
            try Shell.run(path: javaPath, args: args, workDirectory: workDirectory.dirPath) { process in
                guard process.terminationStatus == 0
                else {
                    print(process.terminationReason)
                    return
                }
                Platform.console.info("服务端已停止")
            }
            
            let propertiesFilePath = workDirectory.filePath("server.properties")
            if let propertiesFileConent = try? String(contentsOfFile: propertiesFilePath) {
                Platform.console.pushEphemeral()
                try propertiesFileConent.replacingOccurrences(of: "", with: "")
                    .write(toFile: propertiesFilePath, atomically: false, encoding: .utf8)
                Platform.console.popEphemeral()
                Platform.console.success("服务器运行为离线模式")
            }
            
            
        }
        else {
            try await Shell.run(path: javaPath, args: args, workDirectory: workDirectory.dirPath)
            try await launchServer(filePath, workDirectory: workDirectory)
        }
    }
}
