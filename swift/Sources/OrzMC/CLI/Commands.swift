//
//  File.swift
//  
//
//  Created by joker on 2021/12/21.
//

import SwiftCLI

class Commands: Command {
    let name = "joker"
    let shortDescription = "Says hello to the world"
    
    @Param
    var first: String
    @Param
    var seconde: String?
    
    @CollectedParam
    var remaining: [String]
    
    func execute() throws {
        stdout <<< "Hello world!"
        stdout <<< first
        stdout <<< seconde ?? ""
        stdout <<< remaining.joined(separator: ",")
    }
}
