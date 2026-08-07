class SmartPipeline:

    def run(self, pdf_file):

        self.extract_images()

        self.classify_images()

        self.detect_geometry()

        self.detect_graphs()

        self.detect_photos()

        self.select_models()

        self.upscale()

        self.enhance()

        self.rebuild_pdf()

        self.generate_report()
