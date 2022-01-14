//
//  OrzMC.swift
//  
//
//  Created by wangzhizhou on 2021/12/24.
//

import PaperMC
import JokerKits
import ConsoleKit
import Darwin
import Foundation

@main
struct OrzMC {
    static func main() throws {
        let console = Platform.console
        let input = CommandInput(arguments: CommandLine.arguments)
        let context = CommandContext(console: console, input: input)
        do {
            try console.run(OrzCommandGroup(), with: context)
        }
        catch let error {
            console.error("\(error)")
            exit(1)
        }
    }
}
