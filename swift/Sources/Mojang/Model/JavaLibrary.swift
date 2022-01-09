//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

public struct JavaLibrary: MojangCodable {
    public let downloads: Download
    public let name: String
    public let rules: [Rule]?
    public let natives: [String: String]?
    public let extract: Extract?
    
    public struct Download: MojangCodable {
        public let artifact: Artifact
        public let classifiers: [String: Artifact]?
        
        public struct Artifact: MojangCodable {
            public let path: String
            public let sha1: String
            public let url: URL
            let size: Int64
        }
    }
    
    public struct Rule: MojangCodable {
        public let action: String
        public let os: OS?
        
        public struct OS: MojangCodable {
            public let name: String
        }
    }
    
    public struct Extract: MojangCodable {
        let exclude: [String]
    }
}
