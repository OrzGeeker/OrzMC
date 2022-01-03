//
//  File.swift
//  
//
//  Created by joker on 2022/1/3.
//

import Mojang
import ConsoleKit
import Foundation

final class Launcher: Client {
    
    let console = Terminal()
    
    var startInfo: ClientStartInfo?
    
    func start() async throws {
        
        self.startInfo = try await userInput()
        
        try await self.download()
    }

    public func download() async throws {
        try await downloadClient()
        try await downloadAssets()
        try await downloadLibraries()
    }
}
