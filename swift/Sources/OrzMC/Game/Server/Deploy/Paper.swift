//
//  File.swift
//  
//
//  Created by joker on 2022/1/3.
//

import PaperMC
import JokerKits
import Foundation

enum PaperServerError: Error {
    case versionRespFailed
    case convertBuildStringFailed
    case buildRespFailed
    case applicationFailed
    case downloadURLFailed
}

struct PaperServer: Server {
    
    let deployInfo: DeployInfo
    
    func start() async throws {

        let versionAPI = PaperMC.api.projects("paper").versions(deployInfo.version)
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
        let targetDir = GameDir.server(version: deployInfo.version, type: GameType.paper.rawValue)
        let filePath = targetDir.filePath(filename)
        let progressHint = "下载服务端文件：\(filename)"

        try await GameUtils.download(
            downloadURL,
            progressHint: progressHint,
            targetDir: targetDir,
            hash: application.sha256,
            hashType: .sha256)
        
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

//        Platform.console.output("服务端正在启动请稍等...", style: .success)
//        let process = try await Shell.run(path: javaPath, args: args, workDirectory: targetDir.dirPath)
//        guard process.terminationStatus == 0
//        else {
//            print(process.terminationReason)
//            return
//        }
//        Platform.console.output("服务已终止...", style: .success)
        
        try Shell.run(path: javaPath, args: args, workDirectory: targetDir.dirPath) { process in
            guard process.terminationStatus == 0
            else {
                print(process.terminationReason)
                return
            }
        }
    }
}
