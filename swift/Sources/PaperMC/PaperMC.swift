//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation
import JokerKits

/// ![PaperMC](https://papermc.io/)
public struct PaperMC {
    /// ![PaperMC API v2](https://papermc.io/api/docs/swagger-ui/index.html?configUrl=/api/openapi/swagger-config)
    public struct API {
        
        var pathComponents = [String]()
        
        public init(_ pathComponents: [String] = ["https://papermc.io/api", "v2"]) {
            self.pathComponents = pathComponents
        }
        
        public func projects(_ project: String? = nil) -> API {
            var ret = API(self.pathComponents)
            ret.pathComponents.append("projects")
            if let project = project {
                ret.pathComponents.append(project)
            }
            return ret
        }
        
        public func versions(_ version: String? = nil) -> API {
            var ret = API(self.pathComponents)
            ret.pathComponents.append("versions")
            if let version = version {
                ret.pathComponents.append(version)
            }
            return ret
        }
        
        public func builds(_ build: String? = nil) -> API {
            var ret = API(self.pathComponents)
            ret.pathComponents.append("builds")
            if let build = build {
                ret.pathComponents.append(build)
            }
            return ret
        }
        
        public func downloads(_ download: String? = nil) -> API {
            var ret = API(self.pathComponents)
            ret.pathComponents.append("downloads")
            if let download = download {
                ret.pathComponents.append(download)
            }
            return ret
        }
        
        public func versionFamily(_ family: String) -> API {
            var ret = API(self.pathComponents)
            ret.pathComponents.append("version_group")
            ret.pathComponents.append(family)
            assert(family.count > 0, "family must not be empty")
            return ret
        }
        
        public func versionFamilyBuilds(_ family: String) -> API {
            var ret = API(self.pathComponents)
            ret.pathComponents.append("version_group")
            ret.pathComponents.append(family)
            assert(family.count > 0, "family must not be empty")
            ret.pathComponents.append("builds")
            return ret
        }
        
        public var getData: Data? {
            get async throws {
                let url = String(NSString.path(withComponents: self.pathComponents))
                guard let data = try await URL(string: url)?.getData
                else {
                    return nil
                }
                return data
            }
        }
    }
}

public struct Projects: Codable {
    let projects: [String]
}

public struct Project: Codable {
    public let projectId: String
    public let projectName: String
    public let versionGroups: [String]
    public let versions: [String]
}

public struct Build: Codable {
    public let projectId: String
    public let projectName: String
    public let version: String
    public let build: Int32
    public let time: String
    public let channel: String
    public let promoted: Bool
    public let changes: [Change]
    public let downloads: [String: Download]
}

public struct Change: Codable {
    public let commit: String
    public let summary: String
    public let message: String
}

public struct Download: Codable {
    public let name: String
    public let sha256: String
}

public struct Version: Codable {
    public let projectId: String
    public let projectName: String
    public let version: String
    public let builds: [Int32]
}

public struct VersionFamily: Codable {
    public let projectId: String
    public let projectName: String
    public let versionGroup: String
    public let versions: [String]
}

public struct VersionFamilyBuilds: Codable {
    public let projectId: String
    public let projectName: String
    public let versionGroup: String
    public let versions: [String]
    public let builds: [VersionFamilyBuild]
}

public struct VersionFamilyBuild: Codable {
    public let version: String
    public let build: Int32
    public let time: String
    public let channel: String
    public let promoted: Bool
    public let changes: [Change]
    public let downloads: [String: Download]
}
