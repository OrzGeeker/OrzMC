//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

public struct Logging: MojangCodable {
    public let client: Client
    
    public struct Client: MojangCodable {
        public let argument: String
        public let file: File
        public let type: String
        
        public struct File: MojangCodable {
            public let id: String
            public let sha1: String
            public let url: URL
            let size: Int64
        }
    }
}
