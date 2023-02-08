import { useParams } from 'react-router-dom';
import { Button } from '@mui/material';
import StarRatings from 'react-star-ratings';
import ProgressBar from '@ramonak/react-progress-bar';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Navbar from '../../Components/Navbar';
import DeleteIcon from '@mui/icons-material/Delete';
import React, { useState } from 'react';
import {
    getData,
    postData,
    updateData,
    deleteData,
} from '../../Helpers/helpers.jsx';
import './styles.scss';
import { StoreContext } from '../../Utils/store';
import Login from '../Login';

/*
 * Page that displays recipe information based on its id in the uri, users can rate and comment
 */

const ratings = [5, 4, 3, 2, 1];

function Recipe() {
    const context = React.useContext(StoreContext);
    const { currentUser, navigate } = context;
    const { id } = useParams();

    const [details, setDetails] = useState();
    const [recipe, setRecipe] = useState({});
    const [isAddingReview, setIsAddingReview] = useState(false);
    const [newReview, setNewReview] = useState({ rating: 5, comment: '' });

    const userReview = React.useMemo(
        () =>
            recipe.reviews &&
            recipe.reviews.find(
                (r) => r.user_id === (currentUser && currentUser.id)
            ),
        [recipe, currentUser]
    );

    // fetch current user's recipes
    const fetchRecipes = React.useCallback(() => {
        getData(`http://localhost:8080/api/recipes/${id}`)
            .then((res) => {
                if (!res.ok) throw Error('Could not fetch recipe.');
                return res.json();
            })
            .then((data) => {
                setRecipe(data.recipe);
            })
            .catch((err) => console.error(err));
    }, [id]);

    React.useEffect(() => {
        fetchRecipes();

        const getUserDetails = async () => {
            if (currentUser) {
                const resUser = await getData(
                    'http://127.0.0.1:8080/api/users/' + currentUser.id
                );
                const dataUser = await resUser.json();

                // only signed in users can access this page
                if (dataUser) {
                    setDetails(dataUser);
                } else {
                    setDetails(null);
                }
            }
        };

        getUserDetails();
    }, [fetchRecipes, currentUser]);

    const addReview = () => {
        postData(`http://localhost:8080/api/recipes/review`, {
            firebase_id: currentUser.id,
            recipe_id: id,
            comment: newReview.comment,
            rating: newReview.rating,
        })
            .then((data) => {
                fetchRecipes();
                setIsAddingReview(false);
                setNewReview({ rating: 5, comment: '' });
            })
            .catch((err) => {
                fetchRecipes();
                setIsAddingReview(false);
                console.log(err);
            });
    };

    const editReview = () => {
        updateData(`http://localhost:8080/api/recipes/review`, {
            firebase_id: currentUser.id,
            review_id: userReview.review_id,
            rating: parseInt(newReview.rating),
            comment: newReview.comment,
        })
            .then((data) => {
                fetchRecipes();
                setIsAddingReview(false);
            })
            .catch((err) => {
                fetchRecipes();
                setIsAddingReview(false);
                console.log(err);
            });
    };

    const deleteReview = (review_id = userReview.review_id) => {
        deleteData(`http://localhost:8080/api/recipes/review`, {
            firebase_id: currentUser.id,
            review_id: review_id,
        })
            .then((data) => {
                fetchRecipes();
            })
            .catch((err) => {
                fetchRecipes();
                console.log(err);
            });
    };

    const openAddReview = () => {
        setNewReview({
            rating: userReview ? userReview.rating : 5,
            comment: userReview ? userReview.comment : '',
        });
        setIsAddingReview(true);
    };

    const handleRating = (e) => {
        e.preventDefault();
        if (parseInt(e.target.value) > 5 || parseInt(e.target.value) < 1)
            return;

        setNewReview((pre) => ({ ...pre, rating: e.target.value }));
    };

    return (
        <>
            <Navbar />{' '}
            {!Object.keys(recipe).length && <h1> Recipe not found </h1>}{' '}
            {Object.keys(recipe).length !== 0 && (
                <main className='recipeContainer'>
                    <div className='recipeDetails'>
                        <div className='recipeDescription'>
                            <h1 className='shadowTxt'> {recipe.title} </h1>{' '}
                            <img alt={`${recipe.title}`} src={recipe.image} />{' '}
                            <h3> created by {recipe.username} </h3>{' '}
                            <div>
                                <h2> Ingredients </h2>{' '}
                                {recipe.ingredients.map((ing, i) => (
                                    <div
                                        key={i}
                                        className='recipeDetailsIngredient'
                                    >
                                        {' '}
                                        {ing}{' '}
                                    </div>
                                ))}{' '}
                            </div>{' '}
                            <h2> Time to cook </h2> {recipe.prep_time}
                            &nbsp;minutes{' '}
                        </div>{' '}
                        <div className='recipeMethods'>
                            <h2> Method </h2> <div> {recipe.method} </div>{' '}
                        </div>{' '}
                    </div>{' '}
                    <div className='reviews'>
                        <div className='reviewsSummary'>
                            <h2> Reviews </h2>{' '}
                            <StarRatings
                                rating={recipe.ratings || 0}
                                starRatedColor='#FFA31C'
                                starEmptyColor='#bababa'
                                starDimension='20px'
                                starSpacing='2px'
                                numberofStars={5}
                            />{' '}
                            {' '}
                            {(recipe.ratings || 0).toFixed(1)}{' '}
                            out of 5.0{' '}
                            <p>
                                {' '}
                                {recipe.no_reviews} {' '}
                                total reviews{' '}
                            </p>{' '}
                            <div className='reviewsSummaryStars'>
                                {' '}
                                {ratings.map((rating, i) => (
                                    <div
                                        className='reviewsSummaryStarsBar'
                                        key={i}
                                    >
                                        {' '}
                                        {rating}{' '}
                                        stars{' '}
                                        <ProgressBar
                                            completed={Math.round(
                                                (recipe.reviews.filter(
                                                    (r) => r.rating === rating
                                                ).length /
                                                    (recipe.no_reviews || 1)) *
                                                    100
                                            )}
                                            bgColor='#FFA31C'
                                            baseBgColor='#bababa'
                                            borderRadius='5px'
                                        />
                                    </div>
                                ))}{' '}
                            </div>{' '}
                            <div className='reviewsSummaryWrite'>
                                <h2> Review this recipe </h2>{' '}
                                {details && <Button
                                    color='secondary'
                                    variant='contained'
                                    onClick={openAddReview}
                                >
                                    {' '}
                                    {userReview
                                        ? 'Edit your review'
                                        : 'Write a review'}{' '}
                                </Button>}
                                
                                <br />
                                <br />{' '}
                                {userReview && (
                                    <Button
                                        color='error'
                                        variant='contained'
                                        onClick={() => deleteReview()}
                                    >
                                        Delete your review{' '}
                                    </Button>
                                )}{' '}
                            </div>{' '}
                        </div>{' '}
                        <div className='reviewsAll'>
                            <h2> All reviews </h2>{' '}
                            {!recipe.reviews.length && (
                                <h5> No reviews yet </h5>
                            )}{' '}
                            {recipe.reviews.map((review) => (
                                <div key={review.review_id}>
                                    <h3> {review.username || 'user'} </h3>{' '}
                                    <StarRatings
                                        rating={review.rating || 0}
                                        starRatedColor='#FFA31C'
                                        starEmptyColor='#bababa'
                                        starDimension='20px'
                                        starSpacing='2px'
                                        numberofStars={5}
                                    />{' '}
                                    <p> {review.comment} </p>{' '}
                                    {details && details.is_admin && (
                                        <DeleteIcon
                                            onClick={() =>
                                                deleteReview(review.review_id)
                                            }
                                            fontSize='large'
                                            className='deleteIcon'
                                        />
                                    )}{' '}
                                </div>
                            ))}{' '}
                        </div>{' '}
                    </div>{' '}
                </main>
            )}{' '}
            <Dialog
                open={isAddingReview}
                onClose={() => setIsAddingReview(false)}
            >
                <DialogTitle style={{ width: '500px' }}>
                    {' '}
                    {userReview ? 'Edit your review' : 'Create Review'}{' '}
                </DialogTitle>{' '}
                <DialogContent>
                    <DialogContentText>
                        <b> {recipe.title} </b>{' '}
                    </DialogContentText>{' '}
                    <h2> Overall rating(out of 5) </h2>{' '}
                    <TextField
                        autoFocus
                        margin='normal'
                        type='number'
                        value={newReview.rating}
                        onChange={handleRating}
                        fullWidth
                        variant='standard'
                    />
                    <h2> Written review </h2>{' '}
                    <TextField
                        margin='normal'
                        type='text'
                        value={newReview.comment}
                        onChange={(e) =>
                            setNewReview((pre) => ({
                                ...pre,
                                comment: e.target.value,
                            }))
                        }
                        fullWidth
                        variant='standard'
                        multiline
                        rows={3}
                    />{' '}
                </DialogContent>{' '}
                <DialogActions>
                    <Button onClick={() => setIsAddingReview(false)}>
                        {' '}
                        Cancel{' '}
                    </Button>{' '}
                    {userReview ? (
                        <Button onClick={editReview}> Submit </Button>
                    ) : (
                        <Button onClick={addReview}> Submit </Button>
                    )}{' '}
                </DialogActions>{' '}
            </Dialog>{' '}
        </>
    );
}

export default Recipe;
