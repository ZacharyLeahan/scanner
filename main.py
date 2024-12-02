import twain
import os
from datetime import datetime

def list_twain_scanners():
    try:
        # Initialize TWAIN source manager
        sm = twain.SourceManager(0)
        
        # Get list of available TWAIN sources
        sources = sm.source_list
        
        if not sources:
            print("No TWAIN scanners found")
        else:
            print("Available TWAIN scanners:")
            for source in sources:
                print(f"- {source}")
                
            # Try to get more details about first available scanner
            try:
                source = sm.open_source(sources[0])
                if source:
                    print(f"\nDetailed info for {sources[0]}:")
                    print(f"Identity: {source.identity}")
                    source.close()
            except Exception as e:
                print(f"Could not get detailed info: {str(e)}")
                
        # Clean up
        sm.close()
        
    except Exception as e:
        print(f"Error accessing TWAIN: {str(e)}")

def scan_document(scanner_name="EPSON ES-865", dpi=300, color_mode='color'):
    try:
        # Create output directory if it doesn't exist
        output_dir = "scanned_documents"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Initialize source manager and open source
        sm = twain.SourceManager(0)
        source = sm.open_source(scanner_name)
        
        if source:
            try:
                # Configure scanner settings
                source.set_capability(twain.CAP_FEEDERENABLED, twain.TWTY_BOOL, True)  # Use ADF
                source.set_capability(twain.CAP_DUPLEXENABLED, twain.TWTY_BOOL, True)  # Enable duplex
                source.set_capability(twain.ICAP_XRESOLUTION, twain.TWTY_FIX32, float(dpi))
                source.set_capability(twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, float(dpi))
                
                if color_mode == 'color':
                    source.set_capability(twain.ICAP_PIXELTYPE, twain.TWTY_UINT16, 2)  # RGB
                elif color_mode == 'gray':
                    source.set_capability(twain.ICAP_PIXELTYPE, twain.TWTY_UINT16, 1)  # Grayscale
                elif color_mode == 'bw':
                    source.set_capability(twain.ICAP_PIXELTYPE, twain.TWTY_UINT16, 0)  # Black & White
                
                # Start scanning without UI
                source.request_acquire(0, 0)  # No UI, non-modal
                
                page_count = 0
                while True:
                    # Generate output filename with timestamp and page number
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_file = os.path.join(output_dir, f"scan_{timestamp}_page{page_count+1}.jpg")
                    print(f"Scanning page {page_count+1}...")
                    print(f"Output file: {output_file}")
                    
                    try:
                        # Transfer the image
                        handle = source.xfer_image_natively()[0]
                        if handle:
                            twain.dib_to_bm_file(handle, output_file)
                            page_count += 1
                            print(f"Page {page_count} scanned successfully")
                    except twain.exceptions.DSTransferCancelled:
                        print("No more pages to scan")
                        break
                    except Exception as e:
                        print(f"Error scanning page {page_count+1}: {str(e)}")
                        break
                
                print(f"\nScanning completed. Total pages scanned: {page_count}")
                    
            finally:
                source.close()
        else:
            print(f"Could not open scanner: {scanner_name}")
            
        sm.close()
            
    except Exception as e:
        print(f"Error during scanning: {str(e)}")

if __name__ == "__main__":
    # First list available scanners
    list_twain_scanners()
    
    # Then perform a scan
    print("\nStarting scan operation...")
    scan_document()
