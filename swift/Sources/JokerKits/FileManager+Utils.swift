//
//  File.swift
//  
//
//  Created by joker on 2022/1/3.
//

import Foundation

public extension FileManager {
    static func moveFile(fromFilePath: String, toFilePath: String, overwrite: Bool = false) throws {
        if FileManager.default.fileExists(atPath: toFilePath), overwrite {
            try FileManager.default.removeItem(atPath: toFilePath)
        }
    
        let dirPath = URL(fileURLWithPath: toFilePath).deletingLastPathComponent().path
        if !FileManager.default.fileExists(atPath: dirPath) {
            try dirPath.makeDirIfNeed()
        }
        
        try FileManager.default.moveItem(atPath: fromFilePath, toPath: toFilePath)
    }
}
