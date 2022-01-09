//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

struct Logging: MojangCodable {
    let client: Client
    
    struct Client: MojangCodable {
        let argument: String
        let file: File
        let type: String
        
        struct File: MojangCodable {
            let id: String
            let sha1: String
            let size: Int64
            let url: URL
        }
    }
}
