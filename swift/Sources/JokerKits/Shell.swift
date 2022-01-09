//
//  File.swift
//  
//
//  Created by joker on 2022/1/5.
//

import Foundation

public struct Shell {
    
    @discardableResult
    /// 同步执行Shell命令
    /// - Parameters:
    ///   - path: 命令二进制路径
    ///   - args: 命令参数数组
    /// - Returns: 执行结果字符串
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
    
    @discardableResult
    /// 异步执行Shell命令
    /// - Parameters:
    ///   - path: 命令二进制文件路径
    ///   - args: 命令参数数组
    ///   - terminationHandler: 执行结果回调
    public static func run(path: String, args: [String], terminationHandler:((Process) -> Void)? = nil) throws -> Process {
        let fileURL = URL(fileURLWithPath: path)
        return try Process.run(fileURL, arguments: args, terminationHandler: terminationHandler)
    }
}
