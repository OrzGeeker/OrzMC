//
//  File.swift
//  
//
//  Created by joker on 2022/1/3.
//

import Mojang
import ConsoleKit

extension Launcher {

    func userInput() async throws -> LauncherStartInfo? {
        
        guard let versions = try await Mojang.manifest?.versions
        else {
            return nil
        }
        
        let version = console.choose(
            "👉 选择一个游戏版本".consoleText(.warning),
            from: Array(versions.filter{ $0.type == "release"}[0..<10])) { $0.id.consoleText() }
        console.output("选择的游戏版本：\(version.id)", style: .success)
        
        console.output("输入一个用户名：", style: .warning, newLine: false)
        let username = console.input()
        
        return LauncherStartInfo(
            version: version,
            username: username,
            gameDir: GameDir.clientDir(version: version.id))
    }
}
