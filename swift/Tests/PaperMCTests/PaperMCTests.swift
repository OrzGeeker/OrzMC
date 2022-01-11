import XCTest
@testable import PaperMC

final class PaperMCTests: XCTestCase {
    
    let jsonDecoder = JSONDecoder()
    
    override func setUp() {
        jsonDecoder.keyDecodingStrategy = .convertFromSnakeCase
    }
    
    func testProjects() async throws {
        let data = try await PaperMC.API().projects().getData
        XCTAssertNotNil(data)
        if let data = data {
            XCTAssertNoThrow(try jsonDecoder.decode(Projects.self, from: data))
        }
    }
    
    func testPaper() async throws {
        let paperAPI = PaperMC.API().projects("paper")
        let data = try await paperAPI.getData
        XCTAssertNotNil(data)
        if let data = data {
            let paper = try jsonDecoder.decode(Project.self, from: data)
            XCTAssertNotNil(paper)
            XCTAssert(paper.versions.count > 0)
            let paperVersionAPI = paperAPI.versions(paper.versions.last)
            let data = try await paperVersionAPI.getData
            XCTAssertNotNil(data)
            if let data = data {
                let paperVersion = try jsonDecoder.decode(Version.self, from: data)
                XCTAssertNotNil(paperVersion)
                XCTAssert(paperVersion.builds.count > 0)
                
                let paperVersionBuildAPI = paperVersionAPI.builds("\(paperVersion.builds.last!)")
                let data = try await paperVersionBuildAPI.getData
                XCTAssertNotNil(data)
                if let data = data {
                    let build = try jsonDecoder.decode(Build.self, from: data)
                    XCTAssertNotNil(build)
                    XCTAssert(build.downloads.count > 0)
                    
                    if let name = build.downloads.values.first?.name {
                        let paperVersionBuildDownloadAPI = paperVersionBuildAPI.downloads(name)
                        let data = try await paperVersionBuildDownloadAPI.getData
                        XCTAssertNotNil(data)
                    }
                }
            }
            
            let paperVersionFamilyAPI = paperAPI.versionFamily("1.18")
            let familyData = try await paperVersionFamilyAPI.getData
            XCTAssertNotNil(familyData)
            if let familyData = familyData {
                let versionFamily = try jsonDecoder.decode(VersionFamily.self, from: familyData)
                XCTAssertNotNil(versionFamily)
                XCTAssert(versionFamily.versions.count > 0)
            }
            
            let paperVersionFamilyBuildsAPI = paperAPI.versionFamilyBuilds("1.18")
            let familyBuildsData = try await paperVersionFamilyBuildsAPI.getData
            XCTAssertNotNil(familyBuildsData)
            if let familyBuildsData = familyBuildsData {
                let versionFamilyBuilds = try jsonDecoder.decode(VersionFamilyBuilds.self, from: familyBuildsData)
                XCTAssertNotNil(versionFamilyBuilds)
                XCTAssert(versionFamilyBuilds.builds.count > 0)
            }
        }
    }
}
