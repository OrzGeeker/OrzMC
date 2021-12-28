//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/24.
//

import Foundation
import ConsoleKit
import Mojang

@main
struct OrzMC {
    static func main() async throws {
        let console = Terminal()
        let input = CommandInput(arguments: CommandLine.arguments)
        let context = CommandContext(console: console, input: input)
        
        let commands = Commands(enableAutocomplete: true)
        do {
            let group = commands.group(help: "Group Commands")
            try console.run(group, with: context)
        }
        catch let error {
            console.error("\(error)")
            exit(1)
        }
    }
}
