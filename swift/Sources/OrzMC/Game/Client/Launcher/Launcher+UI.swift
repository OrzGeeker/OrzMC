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
        console.output("选择的游戏版本：".consoleText(.success) + "\(version.id)".consoleText(.info))
        
        console.pushEphemeral()
        console.output("输入游戏用户名：", style: .warning, newLine: false)
        let username = console.input()
        console.popEphemeral()
        console.output("游戏用户名: ".consoleText(.success) + "\(username)".consoleText(.info))
        
        console.pushEphemeral()
        console.output("输入正版帐号".consoleText(.warning) + "(如无可以直接回车)".consoleText(.error) + ": ".consoleText(.warning), newLine: false)
        let accountName = console.input()
        console.popEphemeral()
        
        var accountPassword: String? = nil
        if accountName.count > 0 {
            console.output("正版帐号：".consoleText(.success) + "\(accountName)".consoleText(.info))
            
            console.pushEphemeral()
            console.output("输入正版密码".consoleText(.warning) + "(如无可以直接回车)".consoleText(.error) + ": ".consoleText(.warning), newLine: false)
            accountPassword = console.input(isSecure: false)
            console.popEphemeral()
            
            if let accountPassword = accountPassword {
                let secureText = String(repeating: "*", count: accountPassword.count)
                console.output("正版密码：".consoleText(.success) + secureText.consoleText(.info))
            }
        }
        
        return LauncherStartInfo(
            version: version,
            username: username,
            accountName: accountName,
            accountPassword: accountPassword
        )
    }
}
