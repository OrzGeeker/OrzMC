//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

public struct Download: Codable {
    public let client: Asset
    let clientMappings: Asset
    public let server: Asset
    let serverMappings: Asset
    
    public struct Asset: Codable {
        public let url: URL
        public let sha1: String
        public let size: Int64
    }
}
