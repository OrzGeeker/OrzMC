//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

public struct Manifest: MojangCodable {
    
    public let latest: Latest
    public let versions: [Version]
    
    public struct Latest: MojangCodable {
        let release: String
        let snapshot: String
    }
}
