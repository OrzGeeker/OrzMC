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
    public let rules: [Rule]?
    public let natives: [String: String]?
    
    public struct Download: Codable {
        public let artifact: Artifact
        public let classifiers: Classifiers?
        
        public struct Artifact: Codable {
            public let path: String
            public let sha1: String
            public let url: URL
            let size: Int64
        }
        
        public struct Classifiers: Codable {
            public let javadoc: Artifact
            public let nativesLinux: Artifact
            public let nativesMacos: Artifact
            public let nativesWindows: Artifact
            public let sources: Artifact
        }
    }
    
    public struct Rule: Codable {
        let action: String
        let os: OS?
        
        public struct OS: Codable {
            let name: String
        }
    }
}
