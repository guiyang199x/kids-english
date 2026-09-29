// Prints the text of a PDF, page by page, using macOS's own PDFKit (nothing to install).
// Usage: swift pdftext.swift file.pdf > file.txt
import PDFKit

let url = URL(fileURLWithPath: CommandLine.arguments[1])
guard let doc = PDFDocument(url: url) else {
  FileHandle.standardError.write("Can't open \(url.path)\n".data(using: .utf8)!)
  exit(1)
}
for i in 0..<doc.pageCount {
  print("=== PAGE \(i + 1) ===")
  print(doc.page(at: i)?.string ?? "")
}
