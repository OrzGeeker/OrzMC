//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

public struct JavaLibrary: Codable {
    public let downloads: Download
    public let name: String
    
    public struct Download: Codable {
        public let artifact: Artifact
        
        public struct Artifact: Codable {
            public let path: String
            public let sha1: String
            public let url: URL
            let size: Int64
        }
    }
}
