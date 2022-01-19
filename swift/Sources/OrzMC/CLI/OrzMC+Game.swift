//
//  OrzMC+Game.swift
//  
//
//  Created by joker on 2022/1/15.
//

import Mojang
import JokerKits

extension OrzMC {
    static func chooseGameVersion(_ version: String?) async throws -> Version {
        guard let releaseVersions = try await Mojang.manifest?.versions.filter({ $0.type == "release" })
        else {
            throw GameError.noGameVersions
        }
        let versions = Array(releaseVersions[releaseVersions.startIndex..<releaseVersions.startIndex + 10])
        return versions.filter { $0.id == version }.first ?? OrzMC.chooseFromList(versions, display: { $0.id.consoleText() }, hint: "👉 选择一个游戏版本", completedHint: "选择的游戏版本：")
    }
        
    static func javaPath() throws -> String {
        let javaPath = try Shell.runCommand(with: ["which", "java"]).trimmingCharacters(in: .whitespacesAndNewlines)
        return javaPath
    }
}
