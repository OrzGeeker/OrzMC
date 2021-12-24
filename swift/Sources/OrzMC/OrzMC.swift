//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/24.
//

import Foundation

@main
struct OrzMC {
    static func main() async throws {
        if let manifest = try await Mojang.manifest {
            let gameInfo = try await manifest.versions.first?.gameInfo
            let data = try Mojang.jsonEncoder.encode(gameInfo)
            let jsonString = String(data: data, encoding: .utf8)
            print(jsonString!)
        }
    }
}
