//
//  File.swift
//  
//
//  Created by joker on 2022/1/5.
//

import Foundation

public struct Shell {
    
    @discardableResult
    public static func run(path: String, args: [String]) -> String {
        
        let task = Process()
        
        task.launchPath = path
        task.arguments = args
        
        let pipe = Pipe()
        task.standardOutput = pipe
        task.standardError = pipe
        
        task.launch()
        task.waitUntilExit()
        
        return String(data: pipe.fileHandleForReading.readDataToEndOfFile(), encoding: .utf8)!
    }
}
    
