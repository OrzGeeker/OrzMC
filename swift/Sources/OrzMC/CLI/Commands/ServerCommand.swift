//
//  File.swift
//  
//
//  Created by joker on 2022/1/14.
//

import ConsoleKit
import Dispatch
import JokerKits

struct ServerCommand: Command {
    
    struct Signature: CommandSignature {
        @Flag(name: "debug", short: "d", help: "调试模式")
        var debug: Bool
        
        @Flag(name: "gui", short: "g", help: "服务器以GUI方式启动")
        var gui: Bool
        
        @Flag(name: "force_upgrade", short: "f", help: "强制升级地图")
        var forceUpgrade: Bool
        
        @Option(name: "type", short: "t", help: "服务器类型")
        var type: String?
        
        @Option(name: "version", short: "v", help: "游戏版本号")
        var version: String?
        
        @Option(name: "ms", short: "s", help: "客户端运行使用的最小内存，默认为：512M")
        var minMem: String?
        
        @Option(name: "mx", short: "x", help: "客户端运行使用的最大内存，默认为：2G")
        var maxMem: String?
    }
    
    var help: String = "服务端相关"
    
    func run(using context: CommandContext, signature: Signature) throws {
        try DispatchGroup().syncExecAndWait {
            let version = try await OrzMC.chooseGameVersion(signature.version)
            let gui = signature.gui
            let debug = signature.debug
            let minMem = signature.minMem ?? "512M"
            let maxMem = signature.maxMem ?? "2G"
            let forceUpgrade = signature.forceUpgrade
            
            let serverInfo = ServerInfo(
                version:version.id,
                gui: gui,
                debug: debug,
                forceUpgrade: forceUpgrade,
                minMem: minMem,
                maxMem: maxMem
            )
            
            if let type = GameType(rawValue: signature.type ?? GameType.paper.rawValue) {
                Platform.console.success("服务器类型: \(type)")
                switch type {
                case .paper:
                    try await PaperServer(serverInfo: serverInfo).start()
                case .vanilla:
                    try await VanillaServer(serverInfo: serverInfo).start()
                }
            }
            else{
                Platform.console.success("服务器类型: \(GameType.paper)")
                try await PaperServer(serverInfo: serverInfo).start()
            }
            
        } errorClosure: { error in
            Platform.console.error(error.localizedDescription)
        }
    }
}
