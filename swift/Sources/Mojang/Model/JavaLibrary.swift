//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

struct JavaLibrary: Codable {
    let downloads: Download
    let name: String
    
    struct Download: Codable {
        let artifact: Artifact
        
        struct Artifact: Codable {
            let path: String
            let sha1: String
            let size: Int64
            let url: URL
        }
    }
}
