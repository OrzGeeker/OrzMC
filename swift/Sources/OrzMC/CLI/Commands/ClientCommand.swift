//
//  File.swift
//  
//
//  Created by joker on 2022/1/14.
//

import ConsoleKit
import Dispatch
import JokerKits

struct ClientCommand: Command {
    
    let stopGroup = DispatchGroup()
    
    struct Signature: CommandSignature {
        @Flag(name: "debug", short: "d", help: "调试模式")
        var debug: Bool
        
        @Option(name: "version", short: "v", help: "游戏版本号")
        var version: String?
        
        @Option(name: "username", short: "u", help: "登录用户名")
        var username: String?
    
        @Option(name: "ms", short: "s", help: "客户端运行使用的最小内存，默认为：512M")
        var minMem: String?
        
        @Option(name: "mx", short: "x", help: "客户端运行使用的最大内存，默认为：2G")
        var maxMem: String?
    }
    
    var help: String = "客户端相关命令"
    
    func run(using context: CommandContext, signature: Signature) throws {
        self.stopGroup.enter()
        Task {
            
            let version = try await OrzMC.chooseGameVersion(signature.version)
            
            let username = signature.username ?? OrzMC.userInput(hint: "输入一个用户名：", completedHint: "游戏用户名：")
            
            let debug = signature.debug
            
            let accountName = OrzMC.userInput(hint: "输入正版帐号(如无可以直接回车)：")
            if accountName.count > 0 {
                Platform.console.output("正版帐号：".consoleText(.success) + "\(accountName)".consoleText(.info))
                let accountPassword = OrzMC.userInput(hint: "输入正版密码((如无可以直接回车))：")
                if accountPassword.count > 0 {
                    let secureText = String(repeating: "*", count: accountPassword.count)
                    Platform.console.output("正版密码：".consoleText(.success) + secureText.consoleText(.info))
                }
            }
            
            let minMem = signature.minMem ?? "512M"
            let maxMem = signature.maxMem ?? "2G"
            
            let clientInfo = ClientInfo(
                version: version,
                username: username,
                debug: debug,
                accountName: accountName,
                minMem: minMem,
                maxMem: maxMem
            )

            try await Launcher(clientInfo: clientInfo).start()
            
            self.stopGroup.leave()
        }
        self.stopGroup.wait()
    }
}
