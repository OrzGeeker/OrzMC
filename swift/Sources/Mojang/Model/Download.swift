//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

struct Download: Codable {
    let client: Asset
    let clientMappings: Asset
    let server: Asset
    let serverMappings: Asset
    
    struct Asset: Codable {
        let sha1: String
        let size: Int64
        let url: URL
    }
}
