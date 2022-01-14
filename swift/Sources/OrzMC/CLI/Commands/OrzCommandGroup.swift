//
//  File.swift
//  
//
//  Created by joker on 2022/1/14.
//

import ConsoleKit

struct OrzCommandGroup: CommandGroup {
    var commands: [String : AnyCommand] = [
        "client": ClientCommand(),
        "server": ServerCommand()
    ]
    var help: String = "Minecraft 客户端/服务端部署工具"
}
