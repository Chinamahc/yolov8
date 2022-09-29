import cv2

from ultralytics.yolo.data import MixAndRectDataset, YOLODataset


class Colors:
    # Ultralytics color palette https://ultralytics.com/
    def __init__(self):
        # hex = matplotlib.colors.TABLEAU_COLORS.values()
        hexs = ('FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A', '92CC17', '3DDB86', '1A9334', '00D4BB',
                '2C99A8', '00C2FF', '344593', '6473FF', '0018EC', '8438FF', '520085', 'CB38FF', 'FF95C8', 'FF37C7')
        self.palette = [self.hex2rgb(f'#{c}') for c in hexs]
        self.n = len(self.palette)

    def __call__(self, i, bgr=False):
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h):  # rgb order (PIL)
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))


colors = Colors()  # create instance for 'from utils.plots import colors'


def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    import random

    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(
            img,
            label,
            (c1[0], c1[1] - 2),
            0,
            tl / 3,
            [225, 255, 255],
            thickness=tf,
            lineType=cv2.LINE_AA,
        )


dataset = MixAndRectDataset(dataset=YOLODataset(
    img_path="/d/dataset/COCO/images/val2017",
    img_size=640,
    label_path=None,
    cache_images=False,
    augment=True,
    prefix="",
    rect=False,
    batch_size=4,
    stride=32,
    pad=0.5,
    use_segments=False,
    use_keypoints=False,
))

color = (255, 255, 0)
for d in dataset:
    img = d["img"]
    print(d["im_file"])
    # print(img.shape)
    cls = d["cls"].numpy()
    bboxes = d["bboxes"]

    for i, b in enumerate(bboxes):
        x1, y1, x2, y2 = b
        c = int(cls[i][0])
        # print(x1, y1, x2, y2)
        plot_one_box([int(x1), int(y1), int(x2), int(y2)], img, label=f"{c}", color=colors(c))
    cv2.imshow("p", img)
    if cv2.waitKey(0) == ord("q"):
        break
