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
    
    static func allFiles(in dirPath: String, ext: String) -> [String]? {
        
        guard FileManager.default.fileExists(atPath: dirPath)
        else {
            return nil
        }
        
        var ret = [String]()
        if let enumerator = FileManager.default.enumerator(atPath: dirPath) {
            while let item = enumerator.nextObject() as? String {
                if item.hasSuffix(ext) {
                    let absoluatePath = NSString.path(withComponents: [dirPath, item])
                    ret.append(absoluatePath)
                }
            }
        }
        return ret
    }
}
