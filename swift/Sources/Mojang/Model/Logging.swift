//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

struct Logging: Codable {
    let client: Client
    
    struct Client: Codable {
        let argument: String
        let file: File
        let type: String
        
        struct File: Codable {
            let id: String
            let sha1: String
            let size: Int64
            let url: URL
        }
    }
}
