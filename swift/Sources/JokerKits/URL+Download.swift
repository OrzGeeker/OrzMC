//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/26.
//

import Foundation

#if os(Linux)
import Crypto
#else
import CommonCrypto
#endif

public extension URL {
    var getData: Data? {
        get async throws {
            let (data, response) = try await URLSession.shared.data(from: self)
            guard (response as? HTTPURLResponse)?.statusCode == 200
            else {
                return nil
            }
            return data
        }
    }
    var fileSHA1Value: String {
        get throws {
            guard self.isFileURL
            else {
                throw URLError(.badURL)
            }
            let data = try Data(contentsOf: self)
#if os(Linux)
            
            let digest = Insecure.SHA1.hash(data: data)
            let hexBytes = digest.map { String(format: "%02hhx", $0) }
            
#else
            var digest = [UInt8](repeating: 0, count:Int(CC_SHA1_DIGEST_LENGTH))
            data.withUnsafeBytes {
                _ = CC_SHA1($0.baseAddress, CC_LONG(data.count), &digest)
            }
            let hexBytes = digest.map { String(format: "%02hhx", $0) }
#endif
            
            return hexBytes.joined()
        }
    }
}
