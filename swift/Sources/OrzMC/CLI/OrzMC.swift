//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/24.
//

import Foundation
import Mojang

@main
struct OrzMC {
    static func main() async throws {
        print("Hello, world!")
        
        if let gameInfo = try await Mojang.manifest?.versions.first?.gameInfo?.jsonRepresentation() {
            print(gameInfo)
        }
    }
}
