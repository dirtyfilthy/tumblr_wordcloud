import tumblr
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import tempfile

def make_cloud(blog, tag=None):

	text = tumblr.get_text(blog, tag)
	if not text:
		return None

	wordcloud = WordCloud(width=540, height=540, colormap="jet").generate(text)

	return wordcloud


def save_cloud(blog, tag, directory):
	cloud = make_cloud(blog, tag)
	if not cloud:
		return None
	tf = tempfile.NamedTemporaryFile(delete=False, dir=directory, prefix="tumblr_wordcloud_", suffix='.png')
	filename = tf.name
	tf.close()
	plt.imshow(cloud, interpolation='bilinear')
	plt.axis("off")
	plt.gca().set_axis_off()
	plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
	plt.margins(0,0)
	plt.gca().xaxis.set_major_locator(plt.NullLocator())
	plt.gca().yaxis.set_major_locator(plt.NullLocator())

	plt.savefig(filename, bbox_inches = 'tight',  pad_inches = 0)
	return filename
