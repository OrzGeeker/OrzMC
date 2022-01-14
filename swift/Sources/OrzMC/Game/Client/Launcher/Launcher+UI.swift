//
//  File.swift
//  
//
//  Created by joker on 2022/1/3.
//

import Mojang
import ConsoleKit
import JokerKits

extension Launcher {

    func userInput() async throws -> ClientInfo? {
        
        guard let versions = try await Mojang.manifest?.versions
        else {
            return nil
        }
        
        let version = Platform.console.choose(
            "👉 选择一个游戏版本".consoleText(.warning),
            from: Array(versions.filter{ $0.type == "release"}[0..<10])) { $0.id.consoleText() }
        Platform.console.output("选择的游戏版本：".consoleText(.success) + "\(version.id)".consoleText(.info))
        
        Platform.console.pushEphemeral()
        Platform.console.output("输入游戏用户名：", style: .warning, newLine: false)
        let username = Platform.console.input()
        Platform.console.popEphemeral()
        Platform.console.output("游戏用户名: ".consoleText(.success) + "\(username)".consoleText(.info))
        
        Platform.console.pushEphemeral()
        Platform.console.output("输入正版帐号".consoleText(.warning) + "(如无可以直接回车)".consoleText(.error) + ": ".consoleText(.warning), newLine: false)
        let accountName = Platform.console.input()
        Platform.console.popEphemeral()
        
        var accountPassword: String? = nil
        if accountName.count > 0 {
            Platform.console.output("正版帐号：".consoleText(.success) + "\(accountName)".consoleText(.info))
            
            Platform.console.pushEphemeral()
            Platform.console.output("输入正版密码".consoleText(.warning) + "(如无可以直接回车)".consoleText(.error) + ": ".consoleText(.warning), newLine: false)
            accountPassword = Platform.console.input(isSecure: false)
            Platform.console.popEphemeral()
            
            if let accountPassword = accountPassword {
                let secureText = String(repeating: "*", count: accountPassword.count)
                Platform.console.output("正版密码：".consoleText(.success) + secureText.consoleText(.info))
            }
        }
        
        return ClientInfo(
            version: version,
            username: username,
            accountName: accountName,
            accountPassword: accountPassword
        )
    }
}
