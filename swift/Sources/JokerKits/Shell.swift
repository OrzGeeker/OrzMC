//
//  File.swift
//  
//
//  Created by joker on 2022/1/5.
//

import Foundation

public struct Shell {
    
    static let envPath = "/usr/bin/env"
    
    @discardableResult
    /// 同步执行Shell命令
    /// - Parameters:
    ///   - path: 命令二进制路径
    ///   - args: 命令参数数组
    /// - Returns: 执行结果字符串
    public static func run(path: String, args: [String], workDirectory: String? = nil) throws -> String {
        
        let process = Process()

        process.executableURL = URL(fileURLWithPath: path)
        process.arguments = args
        
        if let workDirectory = workDirectory {
            process.currentDirectoryURL = URL(fileURLWithPath: workDirectory)
        }
        
        let pipe = Pipe()
        process.standardOutput = pipe
        process.standardError = pipe
        
        try process.run()
        process.waitUntilExit()
        
        return String(data: pipe.fileHandleForReading.readDataToEndOfFile(), encoding: .utf8)!
    }
    
    @discardableResult
    /// 异步执行Shell命令
    /// - Parameters:
    ///   - path: 命令二进制文件路径
    ///   - args: 命令参数数组
    ///   - terminationHandler: 执行结果回调
    public static func run(path: String, args: [String], workDirectory: String? = nil, terminationHandler:((Process) -> Void)? = nil) throws -> Process {
        let fileURL = URL(fileURLWithPath: path)
        let process = Process()
        process.executableURL = fileURL
        process.arguments = args
        if let workDirectory = workDirectory {
            process.currentDirectoryURL = URL(fileURLWithPath: workDirectory)
        }
        process.terminationHandler =  terminationHandler
        try process.run()
        
        return process
    }
    

    @discardableResult
    public static func run(path: String, args: [String], workDirectory: String? = nil) async throws -> Process {
        return try await withCheckedThrowingContinuation { continuation in            
            let fileURL = URL(fileURLWithPath: path)
            let process = Process()
            process.executableURL = fileURL
            process.arguments = args
            
            if let workDirectory = workDirectory {
                process.currentDirectoryURL = URL(fileURLWithPath: workDirectory)
            }
            process.terminationHandler =  { process -> Void in
                continuation.resume(returning: process)
            }
            do {
                try process.run()
            }
            catch let error {
                continuation.resume(throwing: error)
            }
        }
    }
    
    
    @discardableResult
    public static func runCommand(with args: [String], workDirectory: String? = nil) async throws -> Process {
        return try await self.run(path: envPath, args: args, workDirectory: workDirectory)
    }
    
    @discardableResult
    public static func runCommand(with args: [String], workDirectory: String? = nil, terminationHandler:((Process) -> Void)? = nil) throws -> Process {
        return try self.run(path: envPath, args: args, workDirectory: workDirectory, terminationHandler: terminationHandler)
    }
    
    @discardableResult
    public static func runCommand(with args: [String], workDirectory: String? = nil) throws -> String {
        return try self.run(path: envPath, args: args, workDirectory: workDirectory)
    }
}
