//
//  QRViewController.swift
//  PyCoin Wallet
//
//  Created by Kevin Kim on 10/12/2019.
//  Copyright © 2019 Kevin Kim. All rights reserved.
//

import UIKit

class QRViewController: UIViewController {
    
    let wallet = Wallet()

    @IBOutlet var imageView: UIImageView!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        drawQR()
    }
    
    func drawQR() {
        if wallet.exportPublicKey.count <= 0 {
            return
        }
        
        let myString = wallet.exportPublicKey
        let data = myString.data(using: String.Encoding.ascii)
        guard let qrFilter = CIFilter(name: "CIQRCodeGenerator") else { return }
        qrFilter.setValue(data, forKey: "inputMessage")
        guard let qrImage = qrFilter.outputImage else { return }
        
        let transform = CGAffineTransform(scaleX: 10, y: 10)
        let scaledQrImage = qrImage.transformed(by: transform)
        
        // Get a CIContext
        let context = CIContext()
        // Create a CGImage *from the extent of the outputCIImage*
        guard let cgImage = context.createCGImage(scaledQrImage, from: scaledQrImage.extent) else { return }
        // Finally, get a usable UIImage from the CGImage
        let processedImage = UIImage(cgImage: cgImage)
        
        imageView.image = processedImage
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
