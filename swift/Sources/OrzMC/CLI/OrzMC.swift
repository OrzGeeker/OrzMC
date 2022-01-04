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
        try await Launcher().start()        
    }
}
