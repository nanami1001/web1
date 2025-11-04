from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from project.forms import RatingForm
from project import db
from project.models import Rating, User, Post

main = Blueprint('main', __name__)

@main.route("/")
def home():
    # Fetch recent ratings to display on the homepage
    ratings = Rating.query.order_by(Rating.id.desc()).all()
    # Fetch latest 3 posts for recommendation
    recent_posts = Post.query.order_by(Post.date_posted.desc()).limit(3).all()
    return render_template("home.html", ratings=ratings, recent_posts=recent_posts)

@main.route("/rate", methods=["GET", "POST"])
def rate():
    if not current_user.is_authenticated:
        flash("請先登入才能使用評價功能", "warning")
        return redirect(url_for('auth.login'))

    form = RatingForm()
    if form.validate_on_submit():
        new_rating = Rating(score=form.score.data,
                            comment=form.comment.data,
                            user_id=current_user.id)
        db.session.add(new_rating)
        db.session.commit()
        flash("評價提交成功！", "success")
        return redirect(url_for('main.home'))
    return render_template("rate.html", form=form)


@main.route('/about')
def about():
    """Render the About page."""
    return render_template('about.html')


@main.route('/rating')
def rating():
    """Render a rating view. Uses the same form as the /rate endpoint but is read-only
    (or can act as an alternate entry point). We pass a RatingForm instance so the
    template's `form` variable is available.
    """
    form = RatingForm()
    return render_template('rating.html', form=form)


@main.route('/location')
def location():
    """Render the location page."""
    return render_template('location.html')
