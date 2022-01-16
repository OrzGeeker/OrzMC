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
}
