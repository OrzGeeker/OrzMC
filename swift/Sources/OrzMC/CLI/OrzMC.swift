//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/24.
//

import PaperMC

@main
struct OrzMC {
    static func main() async throws {
        // 向用户获取启动器相关的参数信息
        if let clientInfo = try await OrzMC.userInput() {
            try await Launcher(clientInfo: clientInfo).start()
        }
//        try await VanillaServer(deployInfo: .init(version: "1.18.1")).start()
//        try await PaperServer(deployInfo: .init(version: "1.18.1")).start()
//        print("Hello, world!")
    }
}

