//
//  File.swift
//  
//
//  Created by joker on 2022/1/4.
//

import Foundation

public extension String {
    func makeDirIfNeed() throws {
        try FileManager.default.createDirectory(atPath: self, withIntermediateDirectories: true)
    }
}
