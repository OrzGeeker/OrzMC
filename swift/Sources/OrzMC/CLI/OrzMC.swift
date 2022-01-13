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
//        try await Launcher().start()
        try await VanillaServer(deployInfo: .init(version: "1.18.1")).start()
        print("Hello, world!")
    }
}

