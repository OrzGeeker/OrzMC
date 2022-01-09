//
//  Downloader.swift
//  
//
//  Created by joker on 2022/1/3.
//

import Foundation

public typealias DownloadProgress = (_ progress: Double, _ filePath: URL?) -> Void

public class Downloader: NSObject {
    
    var downloadTask: URLSessionDownloadTask?
    var progress: DownloadProgress?
    
    public func download(_ url: URL, progress: @escaping DownloadProgress) {
        self.progress = progress
        self.downloadTask = URLSession.shared.downloadTask(with: url)
        self.downloadTask?.delegate = self
        self.downloadTask?.resume()
    }
}

extension Downloader: URLSessionDownloadDelegate {
    public func urlSession(_ session: URLSession, downloadTask: URLSessionDownloadTask, didFinishDownloadingTo location: URL) {
        if let progress = self.progress {
            progress(1, location)
        }
    }
    
    public func urlSession(_ session: URLSession, downloadTask: URLSessionDownloadTask, didWriteData bytesWritten: Int64, totalBytesWritten: Int64, totalBytesExpectedToWrite: Int64) {
        if let progress = self.progress, totalBytesWritten > 0 {
            progress(Double(totalBytesWritten) / Double(totalBytesExpectedToWrite), nil)
        }
    }
}
